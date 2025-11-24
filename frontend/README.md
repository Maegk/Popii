# Creative Fatigue Detection - Frontend

Modern, responsive web UI for the Creative Fatigue Detection System.

## 🚀 Features

- **Modern Dashboard** - Real-time metrics and performance charts
- **Fatigue Monitor** - Visual fatigue detection with radar charts and timelines
- **Creative Management** - AI-powered creative generation interface
- **Dark Mode** - Full dark mode support
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Real-time Updates** - Live data synchronization
- **Smooth Animations** - Framer Motion powered transitions

## 🛠️ Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool & dev server
- **Tailwind CSS** - Utility-first styling
- **Recharts** - Data visualization
- **Framer Motion** - Animations
- **Zustand** - State management
- **React Router** - Navigation
- **Axios** - HTTP client

## 📦 Installation

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

# Start development server
npm run dev
```

The app will be available at `http://localhost:3000`

## 🏗️ Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/       # Reusable UI components
│   │   ├── ui/          # Base UI components (Card, Badge, etc.)
│   │   ├── dashboard/   # Dashboard-specific components
│   │   └── Layout.tsx   # Main layout with sidebar
│   ├── pages/           # Page components
│   │   ├── Dashboard.tsx
│   │   ├── AdSets.tsx
│   │   ├── Creatives.tsx
│   │   ├── FatigueMonitor.tsx
│   │   ├── Analytics.tsx
│   │   └── Settings.tsx
│   ├── lib/             # Utilities
│   │   └── api.ts       # API client
│   ├── store/           # State management
│   │   └── useStore.ts  # Zustand store
│   ├── types/           # TypeScript types
│   │   └── index.ts
│   ├── App.tsx          # App entry point
│   ├── main.tsx         # React entry point
│   └── index.css        # Global styles
├── public/              # Static assets
├── index.html           # HTML template
├── package.json         # Dependencies
├── vite.config.ts       # Vite configuration
├── tailwind.config.js   # Tailwind configuration
└── tsconfig.json        # TypeScript configuration
```

## 🎨 UI Components

### Layout
- Responsive sidebar navigation
- Dark mode toggle
- Mobile-friendly menu

### Dashboard
- Metric cards with trends
- Performance line charts
- Fatigue distribution pie chart
- Recent activity feed

### Fatigue Monitor
- Real-time fatigue scores
- Radar chart for fatigue factors
- Timeline visualization
- Action recommendations

### Creatives
- Creative gallery grid
- AI generation modal
- Performance metrics per creative
- Status management

## 🔌 API Integration

The frontend connects to the backend API at `http://localhost:8000` by default.

Configure the API URL in `.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 🎯 Key Features

### Dark Mode
Click the moon/sun icon in the sidebar to toggle between light and dark themes.

### Real-time Monitoring
Dashboard auto-updates with latest metrics and fatigue scores.

### AI Creative Generation
1. Navigate to Creatives
2. Click "Generate Variations"
3. Select original creative
4. Choose variation types (hook, angle, copy, format)
5. Set number of variations
6. Click Generate

### Fatigue Detection
Visual indicators show fatigue levels:
- 🟢 Green (Low): 0-30%
- 🟡 Yellow (Moderate): 30-60%
- 🟠 Orange (High): 60-80%
- 🔴 Red (Critical): 80-100%

## 📱 Responsive Design

Fully responsive across all devices:
- **Desktop**: Full sidebar + content
- **Tablet**: Collapsible sidebar
- **Mobile**: Hamburger menu

## 🎭 Animations

Smooth transitions powered by Framer Motion:
- Page transitions
- Card animations
- Modal animations
- Hover effects

## 🔐 Environment Variables

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 📄 License

MIT License - see LICENSE file for details
