# Qdrant Frontend

## 🚀 Getting Started

### Prerequisites

- Node.js 18.0.0 or later
- bun package manager
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/qdrant-frontend.git
   cd qdrant-frontend
   ```

2. **Install dependencies**
   Using npm:
   ```bash
   npm install
   ```
   
   Or using yarn:
   ```bash
   yarn
   ```
   
   Or using pnpm:
   ```bash
   pnpm install
   ```
   
   Or using bun:
   ```bash
   bun install
   ```

3. **Environment Setup**
   Create a `.env.local` file in the root directory and add your environment variables:
   ```env
   NEXT_PUBLIC_APP_NAME=Qdrant Frontend
   # Add other environment variables here
   ```

4. **Run the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   # or
   bun dev
   ```

5. **Open your browser**
   The application will be available at [http://localhost:3000](http://localhost:3000)

## 🛠️ Development

### Available Scripts

- `dev` - Start the development server
- `build` - Build the application for production
- `start` - Start the production server
- `lint` - Run ESLint
- `format` - Format code with Prettier

### Project Structure

```
├── app/                    # App router pages and layouts
├── components/             # Reusable UI components
│   ├── ui/                 # Shadcn/ui components
│   └── ...
├── lib/                    # Utility functions and configurations
├── public/                 # Static assets
└── styles/                 # Global styles
```

## 🚀 Deployment

### Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

### Other Platforms

You can also deploy to other platforms that support Next.js:
- [Netlify](https://www.netlify.com/)
- [AWS Amplify](https://aws.amazon.com/amplify/)
- [Railway](https://railway.app/)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Next.js](https://nextjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Tabler Icons](https://tabler-icons.io/)
- [Shadcn/ui](https://ui.shadcn.com/)

---

Made with ❤️ by Your Name
