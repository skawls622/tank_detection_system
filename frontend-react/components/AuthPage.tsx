import { useState } from "react";
import Background from "./ui/Background";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";

<Background src="/app/media/bg.gif" />


type Props = { onBack?: () => void; onSuccess?: () => void };

export default function AuthPage({ onBack, onSuccess }: Props) {
  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);
  const [showPw, setShowPw] = useState(false);
  const [form, setForm] = useState({
    name: "",
    unit: "",
    tank: "",
    rank: "",
    id: "",
    password: "",
    confirmPassword: "",
  });

  const change = (k: keyof typeof form, v: string) =>
    setForm((s) => ({ ...s, [k]: v }));

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (isLogin) {
        const r = await fetch("/api/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ userid: form.id, password: form.password }),
        });
        const j = await r.json();
        if (!j.ok) throw new Error(j.error || "login failed");
      } else {
        if (form.password !== form.confirmPassword)
          throw new Error("비밀번호가 일치하지 않습니다.");
        const r = await fetch("/api/auth/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            name: form.name,
            unit: form.unit,
            tank: form.tank,
            rank: form.rank,
            userid: form.id,
            password: form.password,
          }),
        });
        const j = await r.json();
        if (!j.ok) throw new Error(j.error || "register failed");
      }
      onSuccess?.(); // 성공 시 메인으로
    } catch (err: any) {
      alert(err.message || "요청 실패");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen w-full overflow-hidden">
      {/* 배경 GIF */}
      <Background src="/media/bg.gif" />
      {/* 블러+어둡게 */}
      <div className="absolute inset-0 bg-black/55 backdrop-blur-[2px]" />

      {/* 상단 Back */}
      <div className="relative z-10 p-4 text-white/80">
        <button className="text-sm hover:underline" onClick={() => onBack?.()}>
          ← Back
        </button>
      </div>

      {/* 글래스 카드 */}
      <div className="relative z-10 flex min-h-[calc(100vh-56px)] items-start justify-center p-4">
        <Card className="mx-auto w-full max-w-xl rounded-3xl border-white/20 bg-white/10 text-white backdrop-blur-xl shadow-2xl">
          <CardHeader className="text-center">
            <CardTitle className="text-3xl font-bold">
              {isLogin ? "Login" : "Sign Up"}
            </CardTitle>
            <p className="mt-2 text-sm text-white/70">
              {isLogin
                ? "Sign in to access your dashboard."
                : "Please enter your information accurately for security."}
            </p>
          </CardHeader>
          <CardContent>
            <form className="space-y-4" onSubmit={submit}>
              {!isLogin && (
                <>
                  <Field label="Name" id="name" value={form.name} onChange={(v) => change("name", v)} />
                  <Field label="Unit" id="unit" value={form.unit} onChange={(v) => change("unit", v)} />
                  <Field label="Assigned Tank" id="tank" value={form.tank} onChange={(v) => change("tank", v)} />
                  <Field label="Position" id="rank" value={form.rank} onChange={(v) => change("rank", v)} />
                </>
              )}

              <Field label="ID" id="id" value={form.id} onChange={(v) => change("id", v)} />
              <Field
                label="Password"
                id="password"
                type={showPw ? "text" : "password"}
                value={form.password}
                onChange={(v) => change("password", v)}
                right={
                  <button
                    type="button"
                    className="text-xs text-white/70 hover:text-white"
                    onClick={() => setShowPw((s) => !s)}
                  >
                    {showPw ? "HIDE" : "SHOW"}
                  </button>
                }
              />
              {!isLogin && (
                <Field
                  label="Confirm Password"
                  id="confirm"
                  type="password"
                  value={form.confirmPassword}
                  onChange={(v) => change("confirmPassword", v)}
                />
              )}

              <div className="mt-6">
                <Button
                  type="submit"
                  disabled={loading}
                  className="h-12 w-full rounded-2xl bg-white text-black hover:bg-white/90"
                >
                  {isLogin ? "Login" : "Sign Up"}
                </Button>
              </div>

              <div className="mt-3 text-center text-sm text-white/80">
                {isLogin ? (
                  <>
                    Don’t have an account?{" "}
                    <button
                      type="button"
                      className="underline"
                      onClick={() => setIsLogin(false)}
                    >
                      Sign up
                    </button>
                  </>
                ) : (
                  <>
                    Already have an account?{" "}
                    <button
                      type="button"
                      className="underline"
                      onClick={() => setIsLogin(true)}
                    >
                      Log in
                    </button>
                  </>
                )}
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

function Field({
  label,
  id,
  type = "text",
  value,
  onChange,
  right,
}: {
  label: string;
  id: string;
  type?: string;
  value: string;
  onChange: (v: string) => void;
  right?: React.ReactNode;
}) {
  return (
    <div className="grid gap-2">
      <Label htmlFor={id} className="text-white/90">
        {label}
      </Label>
      <div className="relative">
        <Input
          id={id}
          type={type}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className="h-11 rounded-xl border-white/20 bg-white/15 text-white placeholder:text-white/60"
          placeholder={`Enter your ${label.toLowerCase()}`}
        />
        {right && <div className="absolute inset-y-0 right-3 flex items-center">{right}</div>}
      </div>
    </div>
  );
}
