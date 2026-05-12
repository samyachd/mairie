import { toast } from "sonner";

interface Document {
  numero: string;
  path: string;
}

interface Props {
  doc: Document | undefined | null;
}

export function DocumentLink({ doc }: Props) {
  if (!doc) return <>—</>;

  const handleClick = async () => {
    try {
      await navigator.clipboard.writeText(doc.path);
      toast.success("Chemin copié", {
        description: "Collez-le dans l'Explorateur (Win+E) puis Entrée.",
      });
    } catch {
      toast.error("Impossible de copier", {
        description: doc.path,
      });
    }
  };

  return (
    <button
      type="button"
      onClick={handleClick}
      title={`Copier ${doc.path}`}
      className="text-blue-600 hover:underline cursor-pointer"
    >
      {doc.numero}
    </button>
  );
}
