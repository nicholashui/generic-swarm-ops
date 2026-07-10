export class AppError extends Error {
  constructor(message: string, readonly status = 500, readonly requestId?: string, readonly code?: string) {
    super(message);
  }
}
