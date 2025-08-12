export default function Background({ src }: { src: string }) {
  return (
    <img
      src={src}
      alt=""
      aria-hidden
      className="absolute inset-0 h-full w-full object-cover"
    />
  );
}
