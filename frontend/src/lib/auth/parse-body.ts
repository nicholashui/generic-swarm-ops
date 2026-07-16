/**
 * Read credentials only from POST body — never from query string.
 * Supports JSON and application/x-www-form-urlencoded / multipart form posts.
 */
export async function readPostFields(
  request: Request,
  keys: string[],
): Promise<Record<string, string>> {
  const method = request.method.toUpperCase();
  if (method !== "POST" && method !== "PUT" && method !== "PATCH") {
    throw new Error("Credentials must be sent with POST, not GET");
  }

  // Reject accidental query-string credentials even on POST.
  const url = new URL(request.url);
  for (const key of ["password", "passwd", "secret", "token"]) {
    if (url.searchParams.has(key)) {
      throw new Error("Credentials must not appear in the URL query string");
    }
  }

  const contentType = (request.headers.get("content-type") || "").toLowerCase();
  const out: Record<string, string> = {};

  if (contentType.includes("application/json")) {
    const json = (await request.json().catch(() => null)) as Record<string, unknown> | null;
    if (!json || typeof json !== "object") {
      throw new Error("Invalid JSON body");
    }
    for (const key of keys) {
      const v = json[key];
      out[key] = v == null ? "" : String(v);
    }
    return out;
  }

  // form-urlencoded / multipart (native form submit without JS)
  const form = await request.formData().catch(() => null);
  if (!form) {
    throw new Error("Invalid form body");
  }
  for (const key of keys) {
    const v = form.get(key);
    out[key] = v == null ? "" : String(v);
  }
  return out;
}

export function methodNotAllowedForAuth(): Response {
  return new Response(
    JSON.stringify({
      error: {
        message: "Use HTTP POST with credentials in the body. GET query passwords are rejected.",
        code: "method_not_allowed",
      },
    }),
    {
      status: 405,
      headers: {
        Allow: "POST",
        "Content-Type": "application/json",
      },
    },
  );
}
