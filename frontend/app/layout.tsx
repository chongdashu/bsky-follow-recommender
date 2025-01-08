import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  metadataBase: new URL("https://bsky-follow-recommender.vercel.app"),
  title: {
    default: "BlueSky Follow Recommender - Find People to Follow on BlueSky",
    template: "%s | BlueSky Follow Recommender",
  },
  description:
    "Discover and connect with interesting people on BlueSky. Get personalized recommendations based on your interests and existing follows.",
  keywords: [
    "BlueSky",
    "social network",
    "follow recommendations",
    "social media",
    "networking",
    "community",
  ],
  authors: [{ name: "BlueSky Follow Recommender" }],
  creator: "BlueSky Follow Recommender",
  publisher: "BlueSky Follow Recommender",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    title: "BlueSky Follow Recommender - Find People to Follow on BlueSky",
    description:
      "Discover and connect with interesting people on BlueSky. Get personalized recommendations based on your interests and existing follows.",
    url: "https://bsky-follow-recommender.vercel.app",
    siteName: "BlueSky Follow Recommender",
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "BlueSky Follow Recommender - Find People to Follow on BlueSky",
    description:
      "Discover and connect with interesting people on BlueSky. Get personalized recommendations based on your interests and existing follows.",
    creator: "@bskyrecommender",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "white" },
    { media: "(prefers-color-scheme: dark)", color: "black" },
  ],
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="icon" href="/favicon.ico" sizes="any" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <link rel="manifest" href="/manifest.json" />
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased min-h-screen`}
      >
        {children}
      </body>
    </html>
  );
}
