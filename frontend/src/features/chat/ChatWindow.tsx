import { useState, useEffect, useRef } from 'react'
import { useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { chatAPI } from '../../api/chat'
import { useAuthStore } from '../../stores/authStore'
import { Message } from '../../types'
import Card from '../../components/common/Card'
import Input from '../../components/common/Input'
import Button from '../../components/common/Button'
import { Send } from 'lucide-react'

export default function ChatWindow() {
  const { conversationId } = useParams()
  const { user } = useAuthStore()
  const [messageContent, setMessageContent] = useState('')
  const [localMessages, setLocalMessages] = useState<Message[]>([])
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useQuery({
    queryKey: ['conversation', conversationId],
    queryFn: () => chatAPI.getConversation(conversationId!),
    enabled: !!conversationId,
  })

  const { data: messages = [] } = useQuery({
    queryKey: ['messages', conversationId],
    queryFn: () => chatAPI.getMessages(conversationId!),
    enabled: !!conversationId,
  })

  useEffect(() => {
    setLocalMessages(messages)
  }, [messages])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [localMessages])

  const handleSendMessage = async () => {
    if (!messageContent.trim() || !conversationId) return

    try {
      const newMessage = await chatAPI.sendMessage(conversationId, messageContent)
      setLocalMessages([...localMessages, newMessage])
      setMessageContent('')
    } catch (error) {
      console.error('Failed to send message:', error)
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 h-screen flex flex-col">
      <Card className="flex-1 flex flex-col p-0 overflow-hidden">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {localMessages.map((msg) => (
            <div
              key={msg.id}
              className={`flex ${msg.sender_id === user?.id ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs px-4 py-2 rounded-lg ${
                  msg.sender_id === user?.id
                    ? 'bg-primary text-white'
                    : 'bg-neutral-100 text-neutral-900'
                }`}
              >
                <p className="break-words">{msg.content}</p>
                <span className="text-xs opacity-60 mt-1 block">
                  {new Date(msg.created_at).toLocaleTimeString()}
                </span>
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="border-t p-4 flex gap-2">
          <Input
            placeholder="Type a message..."
            value={messageContent}
            onChange={(e) => setMessageContent(e.target.value)}
            onKeyPress={(e) =>
              e.key === 'Enter' && !e.shiftKey && handleSendMessage()
            }
          />
          <Button onClick={handleSendMessage} size="md">
            <Send size={20} />
          </Button>
        </div>
      </Card>
    </div>
  )
}
