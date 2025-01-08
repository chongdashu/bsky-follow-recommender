import type { Metadata } from "next";
import { redirect } from "next/navigation";

export const metadata: Metadata = {
  title: "Welcome to BlueSky Follow Recommender",
  description:
    "Get started finding interesting people to follow on BlueSky. Connect your account to receive personalized recommendations.",
  openGraph: {
    title: "Welcome to BlueSky Follow Recommender",
    description:
      "Get started finding interesting people to follow on BlueSky. Connect your account to receive personalized recommendations.",
  },
};

export default function Home() {
  redirect("/login");
}
