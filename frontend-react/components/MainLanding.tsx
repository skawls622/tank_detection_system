import Background from "./ui/Background";
import { Button } from "./ui/button";

export default function MainLanding({ onGetStarted }: { onGetStarted?: () => void }) {
  return (
    <div className="relative min-h-screen w-full overflow-hidden">
      {/* ✅ public/media → /app/media 로 접근 */}
      <Background src="/app/media/bg.gif" />
      <div className="absolute inset-0 bg-black/55" />
      <div className="relative z-10 flex min-h-screen items-center justify-center">
        <div className="flex flex-col items-center gap-6">
          <img src="/app/media/logo.png" alt="logo" className="h-48 w-48 object-contain drop-shadow-[0_8px_24px_rgba(0,0,0,0.6)]" />
          <Button size="lg" className="px-10 text-base tracking-widest" onClick={() => onGetStarted?.()}>
            START
          </Button>
        </div>
      </div>
    </div>
  );
}
