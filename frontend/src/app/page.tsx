import { redirect } from "next/navigation";

/**
 * The workspace is the entry point: `/` skips the marketing landing page and
 * goes straight to a new chat. Auth and setup are resolved by the workspace
 * layout, which sends unauthenticated visitors to the login page.
 * The landing page lives at `/home`.
 */
export default function RootPage() {
  redirect("/workspace");
}
