import { LoginForm } from "@/components/auth/login-form";

/**
 * Login page component that renders the login form
 * Using server component by default since this is a Next.js page
 */
export default function LoginPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4">
      <LoginForm />
      <p className="mt-8 text-sm text-muted-foreground text-center max-w-md">
        Note: You&apos;ll need to use your BlueSky app password, not your
        account password. You can create one in your BlueSky account settings.
      </p>
    </div>
  );
}
