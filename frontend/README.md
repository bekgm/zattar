# Zattar Frontend

Modern React+TypeScript marketplace frontend for Kazakhstan.

## Tech Stack

- React 18 with TypeScript
- Vite (fast build tool)
- React Router v6
- TanStack Query (server state)
- Zustand (client state)
- TailwindCSS (styling)
- Framer Motion (animations)
- Lucide React (icons)

## Project Structure

```
src/
├── api/                  # API client functions
├── components/           # Reusable UI components
│   ├── common/          # Generic components (Button, Card, Input, Alert)
│   └── layouts/         # Layout components (Header, Footer, MainLayout)
├── features/            # Feature modules
│   ├── listings/        # Listing browse, detail, create
│   ├── chat/            # Chat conversations & messaging
│   └── deals/           # Safe Deal flow
├── hooks/               # Custom React hooks
├── router/              # Route configuration
├── stores/              # Zustand stores (auth, ui, chat)
├── styles/              # Global styles & design tokens
├── types/               # TypeScript types
├── utils/               # Utility functions
├── App.tsx              # Main App component
└── main.tsx             # Entry point
```

## Design System

### Colors
- **Primary (Brown):** #8B5E3C
- **Dark Brown:** #5C3A21
- **Light Background:** #F5F1EC
- **Success:** #16A34A
- **Error:** #DC2626

### Components
- Rounded buttons (8-12px)
- Soft shadows
- Smooth transitions
- Mobile-first responsive

## Getting Started

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Splash Screen

Animated splash screen displays on first visit with:
- Centered "Zattar" logo
- Brown theme gradient
- Animated loading bar
- 2-second duration
- Auto-hidden via localStorage flag