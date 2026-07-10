import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";
export function middleware(request: NextRequest) {
  if (process.env.NEXT_PUBLIC_DEMO_MODE !== "false") return NextResponse.next();
  if (request.nextUrl.pathname.startsWith("/app") && !request.cookies.get("frontend_session")) {
    const loginUrl = new URL("/login", request.url);
    return NextResponse.redirect(loginUrl);
  }
  return NextResponse.next();
}
export const config = { matcher: ["/app/:path*"] };
