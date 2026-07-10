function describePath(pathSegments) {
  if (pathSegments.length === 0) {
    return "$";
  }
  return `$${pathSegments.map((segment) => (typeof segment === "number" ? `[${segment}]` : `.${segment}`)).join("")}`;
}

function isPlainObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

function actualType(value) {
  if (Array.isArray(value)) {
    return "array";
  }
  if (value === null) {
    return "null";
  }
  return typeof value;
}

function validateObject(schema, value, pathSegments, errors) {
  if (!isPlainObject(value)) {
    errors.push(`${describePath(pathSegments)} must be an object`);
    return;
  }

  const required = Array.isArray(schema.required) ? schema.required : [];
  for (const key of required) {
    if (!(key in value)) {
      errors.push(`${describePath(pathSegments)} is missing required property "${key}"`);
    }
  }

  const properties = isPlainObject(schema.properties) ? schema.properties : {};
  for (const [key, propertySchema] of Object.entries(properties)) {
    if (key in value) {
      validateValue(propertySchema, value[key], [...pathSegments, key], errors);
    }
  }
}

function validateArray(schema, value, pathSegments, errors) {
  if (!Array.isArray(value)) {
    errors.push(`${describePath(pathSegments)} must be an array`);
    return;
  }

  if (typeof schema.minItems === "number" && value.length < schema.minItems) {
    errors.push(`${describePath(pathSegments)} must contain at least ${schema.minItems} item(s)`);
  }

  if (typeof schema.maxItems === "number" && value.length > schema.maxItems) {
    errors.push(`${describePath(pathSegments)} must contain at most ${schema.maxItems} item(s)`);
  }

  if (schema.items) {
    value.forEach((item, index) => {
      validateValue(schema.items, item, [...pathSegments, index], errors);
    });
  }
}

function validateNumber(schema, value, pathSegments, errors) {
  if (typeof value !== "number" || Number.isNaN(value)) {
    errors.push(`${describePath(pathSegments)} must be a number`);
    return;
  }

  if (typeof schema.minimum === "number" && value < schema.minimum) {
    errors.push(`${describePath(pathSegments)} must be >= ${schema.minimum}`);
  }

  if (typeof schema.maximum === "number" && value > schema.maximum) {
    errors.push(`${describePath(pathSegments)} must be <= ${schema.maximum}`);
  }
}

function validateString(schema, value, pathSegments, errors) {
  if (typeof value !== "string") {
    errors.push(`${describePath(pathSegments)} must be a string`);
    return;
  }

  if (typeof schema.minLength === "number" && value.length < schema.minLength) {
    errors.push(`${describePath(pathSegments)} must be at least ${schema.minLength} character(s)`);
  }

  if (schema.format === "date-time" && Number.isNaN(Date.parse(value))) {
    errors.push(`${describePath(pathSegments)} must be a valid date-time string`);
  }

  if (schema.format === "date" && !/^\d{4}-\d{2}-\d{2}$/.test(value)) {
    errors.push(`${describePath(pathSegments)} must be a YYYY-MM-DD date`);
  }
}

export function validateValue(schema, value, pathSegments = [], errors = []) {
  if (!isPlainObject(schema)) {
    errors.push(`${describePath(pathSegments)} has an invalid schema definition`);
    return errors;
  }

  if (Array.isArray(schema.enum) && !schema.enum.includes(value)) {
    errors.push(`${describePath(pathSegments)} must be one of: ${schema.enum.join(", ")}`);
    return errors;
  }

  switch (schema.type) {
    case "object":
      validateObject(schema, value, pathSegments, errors);
      break;
    case "array":
      validateArray(schema, value, pathSegments, errors);
      break;
    case "number":
      validateNumber(schema, value, pathSegments, errors);
      break;
    case "integer":
      if (!Number.isInteger(value)) {
        errors.push(`${describePath(pathSegments)} must be an integer`);
      } else {
        validateNumber(schema, value, pathSegments, errors);
      }
      break;
    case "boolean":
      if (typeof value !== "boolean") {
        errors.push(`${describePath(pathSegments)} must be a boolean`);
      }
      break;
    case "string":
      validateString(schema, value, pathSegments, errors);
      break;
    default:
      errors.push(`${describePath(pathSegments)} uses unsupported schema type "${schema.type}"`);
      break;
  }

  return errors;
}

export function validateAgainstSchema(schema, value) {
  const errors = validateValue(schema, value, [], []);
  return {
    valid: errors.length === 0,
    errors
  };
}

export function assertValidAgainstSchema(schema, value, label) {
  const result = validateAgainstSchema(schema, value);
  if (!result.valid) {
    const heading = label ? `${label} failed validation` : "Schema validation failed";
    throw new Error(`${heading}\n- ${result.errors.join("\n- ")}`);
  }
  return true;
}

export function describeSchemaTypes(schema) {
  if (!isPlainObject(schema)) {
    return [];
  }

  const discovered = new Set();
  function walk(node) {
    if (!isPlainObject(node)) {
      return;
    }
    if (node.type) {
      discovered.add(node.type);
    }
    if (node.items) {
      walk(node.items);
    }
    if (isPlainObject(node.properties)) {
      for (const child of Object.values(node.properties)) {
        walk(child);
      }
    }
  }

  walk(schema);
  return [...discovered];
}
