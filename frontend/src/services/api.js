import axios from "axios";

const api = axios.create({
  baseURL:
    import.meta.env.VITE_API_BASE_URL ??
    "http://127.0.0.1:8000",
  timeout: 30000,
});

export async function analyseCase(caseData) {
  const response = await api.post(
    "/api/v1/analyse",
    caseData,
  );

  return response.data;
}