const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

async function handleResponse(res: Response) {
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || "Terjadi kesalahan pada server");
  }
  return res.json();
}

export async function createFund(data: {
  name: string;
  gp_name?: string;
  fund_type?: string;
  vintage_year?: number;
}) {
  const res = await fetch(`${BASE_URL}/funds`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return handleResponse(res);
}

export async function getFunds() {
  const res = await fetch(`${BASE_URL}/funds`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
    cache: "no-store",
  });
  return handleResponse(res);
}

export async function getFundById(id: number) {
  const res = await fetch(`${BASE_URL}/funds/${id}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
    cache: "no-store",
  });
  return handleResponse(res);
}

export async function uploadDocument(file: File, fund_id: number) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("fund_id", String(fund_id));

  const res = await fetch(`${BASE_URL}/documents/upload`, {
    method: "POST",
    body: formData,
  });

  return handleResponse(res);
}

export async function sendChatMessage(message: string, fund_id?: number | null) {
  const payload: Record<string, any> = { query: message };
  if (fund_id) payload.fund_id = fund_id;

  const res = await fetch(`${BASE_URL}/chat/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  return handleResponse(res);
}

export async function getTransactions(fundId: number) {
  const res = await fetch(`${BASE_URL}/funds/${fundId}/transactions/all`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || "Gagal mengambil data transaksi");
  }
  return res.json();
}

export async function getFundMetrics(fundId: number) {
  const res = await fetch(`${BASE_URL}/funds/${fundId}/metrics`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
    cache: "no-store",
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || "Gagal mengambil data metrics");
  }

  return res.json();
}

export async function deleteFund(fundId: number) {
  const res = await fetch(`${BASE_URL}/funds/${fundId}`, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
  });
  return handleResponse(res);
}
