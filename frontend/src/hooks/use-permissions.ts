import { hasPermission } from "@/lib/auth/permissions";
import type { AppRole, Permission } from "@/types/permissions";
export function usePermissions(role: AppRole) { return { can: (permission: Permission) => hasPermission(role, permission) }; }
