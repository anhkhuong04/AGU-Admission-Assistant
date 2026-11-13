import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AGU Admission Assistant — Development",
  description: "Môi trường phát triển dự án hỗ trợ tra cứu tuyển sinh độc lập.",
  robots: { index: false, follow: false },
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="vi">
      <body>
        <a className="skip-link" href="#main">
          Đến nội dung chính
        </a>
        {children}
      </body>
    </html>
  );
}
