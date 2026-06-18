import './globals.css';

export const metadata = {
  title: 'MediBot — Hospital Knowledge Assistant',
  description: 'AI-powered hospital knowledge assistant with role-based access control, hybrid RAG, and SQL RAG capabilities.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
