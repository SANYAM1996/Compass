import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ||
  "https://carne-compass-api-c9fvgtbub7efcxgy.northeurope-01.azurewebsites.net";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 120000,
});

export async function analyseCase(caseData) {
  const response = await api.post(
    "/api/v1/analyse",
    caseData,
  );

  return response.data;
}