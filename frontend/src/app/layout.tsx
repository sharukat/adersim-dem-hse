import './globals.css'
import { Inter } from 'next/font/google'
import { Providers } from "./providers";
import Navigationbar from '@/components/Navigationbar'
import Footer from '@/components/Footer';

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: 'ADERSIM | AI Assistant',
  description: 'LLM-based drink driving awareness tool',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="!scroll-smooth">
      <body className={inter.className}>
        <Providers>
          <div className="w-[80%]">
            <Navigationbar />
          </div>
          <main>
            {children}
          </main>
          <Footer />

        </Providers>
      </body>
    </html>
  )
}