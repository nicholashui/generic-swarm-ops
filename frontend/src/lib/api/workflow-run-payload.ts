/**
 * Build a minimal valid run payload from a workflow input_schema.
 * Used by Run now so required fields (e.g. case_id) are always present.
 */

export type WorkflowSchemaLike = {
  id?: string;
  input_schema?: {
    type?: string;
    required?: string[];
    properties?: Record<string, { type?: string; default?: unknown }>;
  } | null;
};

function defaultForProperty(name: string, prop?: { type?: string; default?: unknown }): unknown {
  if (prop && "default" in prop && prop.default !== undefined) return prop.default;
  const t = prop?.type || "string";
  if (t === "number" || t === "integer") return 0;
  if (t === "boolean") return false;
  if (t === "array") return [];
  if (t === "object") return {};
  // string defaults with common operational keys
  if (name === "case_id") return `case_${Date.now().toString(36)}`;
  if (name === "customer_name") return "Demo Customer";
  if (name === "triggered_from") return "frontend_run_now";
  return `${name}_value`;
}

export function buildWorkflowRunPayload(
  workflow: WorkflowSchemaLike | null | undefined,
  extras: Record<string, unknown> = {},
): Record<string, unknown> {
  const schema = workflow?.input_schema || {
    type: "object",
    required: ["case_id"],
    properties: {
      case_id: { type: "string" },
      triggered_from: { type: "string" },
    },
  };
  const required = Array.isArray(schema.required) ? schema.required : [];
  const properties = schema.properties || {};
  const payload: Record<string, unknown> = { ...extras };

  for (const field of required) {
    if (payload[field] === undefined || payload[field] === null || payload[field] === "") {
      payload[field] = defaultForProperty(field, properties[field]);
    }
  }

  // Always stamp UI origin when not provided
  if (payload.triggered_from === undefined) {
    payload.triggered_from = extras.triggered_from || "frontend_run_now";
  }

  return payload;
}
