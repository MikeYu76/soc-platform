const API_ROOT = "/api";

export async function request(path, options = {}) {
  const token = localStorage.getItem("soc_token");
  const headers = new Headers(options.headers || {});
  if (options.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  if (token) headers.set("Authorization", "Bearer " + token);

  const response = await fetch(API_ROOT + path, { ...options, headers });
  const text = await response.text();
  let payload = null;
  if (text) {
    try {
      payload = JSON.parse(text);
    } catch {
      payload = text;
    }
  }
  if (!response.ok) {
    const detail = payload && typeof payload === "object" ? payload.detail : null;
    throw new Error(detail || response.statusText || "Request failed");
  }
  return payload;
}

export const api = {
  me: () => request("/auth/me"),
  login: (username, password) =>
    request("/auth/login", {
      method: "POST",
      body: JSON.stringify({ username, password }),
    }),
  cases: (params = "") => request("/cases?limit=100&offset=0" + params),
  case: (id) => request("/cases/" + encodeURIComponent(id)),
  timeline: (id) => request("/cases/" + encodeURIComponent(id) + "/timeline"),
  alerts: (params = "") => request("/alerts?limit=100&offset=0" + params),
  events: (params = "") => request("/events?limit=100&offset=0" + params),
  caseAction: (id, action, body) =>
    request("/cases/" + encodeURIComponent(id) + "/" + action, {
      method: action === "priority" || action === "assign" || action === "start" || action === "resolve" || action === "close" ? "PATCH" : "POST",
      body: body ? JSON.stringify(body) : undefined,
    }),
  addComment: (id, body) =>
    request("/cases/" + encodeURIComponent(id) + "/comments", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  addEvidence: (id, body) =>
    request("/cases/" + encodeURIComponent(id) + "/evidence", {
      method: "POST",
      body: JSON.stringify(body),
    }),
  alertAction: (id, action, body) =>
    request("/alerts/" + encodeURIComponent(id) + "/" + action, {
      method: "PATCH",
      body: body ? JSON.stringify(body) : undefined,
    }),
};
