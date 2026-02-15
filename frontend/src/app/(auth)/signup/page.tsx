import { SignUpForm } from '@/components/auth/SignUpForm';

export default function SignUpPage() {
  return (
    <div className="mt-8">
      <h2 className="text-2xl font-bold text-center text-gray-900 mb-6">
        Create your account
      </h2>
      <SignUpForm />
    </div>
  );
}
