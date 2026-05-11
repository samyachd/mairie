import { useState } from "react";
import { QrCode } from "lucide-react";
import { toast } from "sonner";
import api from "@/app/services/api";
import { Button } from "@/app/components/ui/button";

interface Props {
  endpoint: string;
  filename: string;
  label?: string;
}

export function QrDownloadButton({ endpoint, filename, label }: Props) {
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
    setLoading(true);
    try {
      const res = await api.get(endpoint, { responseType: "blob" });
      const url = URL.createObjectURL(res.data);
      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (e) {
      console.error("QR code error:", e);
      toast.error("Impossible de générer le QR code");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Button
      variant="outline"
      size="sm"
      onClick={handleClick}
      disabled={loading}
      title="Télécharger le QR code"
    >
      <QrCode className="h-4 w-4 mr-1" />
      {label ? (loading ? "Chargement…" : label) : (loading ? "…" : "")}
    </Button>
  );
}
