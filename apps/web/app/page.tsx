export default function Home() {
  return (
    <div className="shell">
      <header className="masthead">
        <span className="wordmark">AGU Admission Assistant</span>
        <span className="environment">Development</span>
      </header>
      <main id="main" tabIndex={-1}>
        <p className="eyebrow">Nền tảng đang được xây dựng</p>
        <h1>
          Thông tin đúng nguồn.
          <br />
          Tư vấn có căn cứ.
        </h1>
        <p className="intro">
          Dự án độc lập hỗ trợ tra cứu tuyển sinh đại học chính quy Trường Đại
          học An Giang. Đây là môi trường phát triển, chưa cung cấp chatbot hoặc
          thông tin tuyển sinh đã kiểm duyệt.
        </p>
        <a className="official-link" href="https://tuyensinh.agu.edu.vn/">
          Xem cổng tuyển sinh chính thức của AGU{" "}
          <span aria-hidden="true">↗</span>
        </a>
        <aside className="notice" aria-label="Phạm vi dự án">
          <h2>Về môi trường này</h2>
          <p>
            Chưa tiếp nhận câu hỏi, hồ sơ hay thông tin cá nhân. Dự án chưa được
            AGU phê duyệt hoặc bảo trợ và không xác nhận kết quả xét tuyển.
          </p>
        </aside>
      </main>
      <footer>Website độc lập · Bản phát triển local</footer>
    </div>
  );
}
