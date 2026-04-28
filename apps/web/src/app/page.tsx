import { redirect } from "next/navigation";

/** Root page — redirect to the social feed. */
export default function Home() {
  redirect("/feed");
}
