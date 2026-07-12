import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

export async function analyseCase(caseData) {
  const response = await api.post(
    "/api/v1/analyse",
    caseData,
  );

  return response.data;
}