# Frontend

Next.js frontend for the Qdrant Hackathon music video processing platform.

> **Note**: For complete project setup and overview, see the [main README](../README.md) in the project root.

## Quick Start

1. **Install**: `bun install` (or npm/yarn/pnpm install)
2. **Run**: `bun dev` (or npm/yarn/pnpm run dev)
3. **Open**: `http://localhost:3000`

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS
- **UI Libraries**: [Shadcn UI](https://ui.shadcn.com/), [Aceternity UI](https://ui.aceternity.com/)
- **Animations**: Framer Motion

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd qdrant-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   # or
   pnpm install
   # or
   bun install
   ```

## Development

1. Start the development server:
   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   # or
   bun dev
   ```

2. Open [http://localhost:3000](http://localhost:3000) in your browser to view the application.

3. The application will automatically reload when you make changes to the source files.

## Using Shadcn UI Components

This project uses [Shadcn UI](https://ui.shadcn.com/), a collection of reusable components built using Radix UI and Tailwind CSS.

### Adding New Components

To add a new Shadcn component:

```bash
npx shadcn-ui@latest add <component-name>
# Example:
# npx shadcn-ui@latest add button
# npx shadcn-ui@latest add dropdown-menu
```

This will:
1. Add the component to `components/ui/`
2. Update any necessary dependencies
3. Make the component ready to import and use in your application

### Using Components

Import and use components like this:

```tsx
import { Button } from "@/components/ui/button"

export default function Home() {
  return (
    <div>
      <Button>Click me</Button>
    </div>
  )
}
```

### Theming

This project uses the `new-york` style from Shadcn UI. You can customize the theme in the following files:
- `app/globals.css` - Contains the base styles and theme variables
- `components/theme-provider.tsx` - Handles theme switching (light/dark mode)
- `tailwind.config.js` - Contains the Tailwind CSS configuration

## Using Aceternity UI Components

This project also includes [Aceternity UI](https://ui.aceternity.com/), a collection of beautiful, animated UI components built with Framer Motion and Tailwind CSS.

### Installation

Aceternity UI components are already installed in this project. If you need to add new components, you can install them using the instructions in the website


### Using Components

Import and use Aceternity UI components like this:

```tsx
'use client';
import { WobbleCard } from "@/components/ui/wobble-card";

export default function Home() {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 max-w-7xl mx-auto w-full">
      <WobbleCard>
        <h2 className="text-2xl font-bold">Aceternity UI</h2>
        <p className="mt-2 text-sm">Beautiful, animated UI components</p>
      </WobbleCard>
    </div>
  )
}
```

### Available Components

Some of the available Aceternity UI components include:
- Animated backgrounds
- Card effects
- Hover effects
- Navigation components
- And many more...

Visit the [Aceternity UI documentation](https://ui.aceternity.com/docs) for a complete list of components and their usage.

## Building for Production

To create a production build:

```bash
npm run build
# or
yarn build
# or
pnpm build
# or
bun run build
```

To start the production server:

```bash
npm start
# or
yarn start
# or
pnpm start
# or
bun start
```
