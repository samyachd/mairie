import { useState, useCallback } from "react";
import { Upload, X } from "lucide-react";
import { toast } from "sonner";
import { extractFromFile, type OcrExtractedData } from "@/app/services/document";

const FIELD_LABELS: Record<string, string> = {
  type_document: "Type de document",
  fournisseur: "Fournisseur",
  marque: "Marque",
  numero_document: "N° document",
  numero_de_commande: "N° de commande",
  tag: "Tag / N° série",
  date_document: "Date du document",
  date_achat: "Date d'achat",
  fin_garantie: "Fin de garantie",
  montant_ttc: "Montant TTC",
  montant_ht: "Montant HT",
  type_equipement: "Type d'équipement",
};

export function Ocr() {
  const [pending, setPending] = useState(false);
  const [dragging, setDragging] = useState(false);
  const [result, setResult] = useState<OcrExtractedData | null>(null);

  const handleFile = async (file: File) => {
    setPending(true);
    setResult(null);
    try {
      const response = await extractFromFile(file);
      setResult(response.donnees);
      const filled = Object.values(response.donnees).filter((v) => v != null).length;
      toast.success("Document analysé", {
        description: `${filled} champ${filled > 1 ? "s" : ""} extrait${filled > 1 ? "s" : ""}.`,
      });
    } catch (e) {
      toast.error("Échec de l'analyse OCR", {
        description: e instanceof Error ? e.message : "Erreur inconnue",
      });
    } finally {
      setPending(false);
    }
  };

  const onDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  }, []);

  const entries = result
    ? Object.entries(result).filter(([, v]) => v != null)
    : [];

  return (
    <div className="flex flex-col items-center justify-center min-h-[75vh] gap-8">
      <div className="text-center">
        <h1 className="text-2xl font-bold">Analyse OCR</h1>
        <p className="text-sm text-muted-foreground mt-1">
          Déposez un fichier pour extraire automatiquement les informations du document
        </p>
      </div>

      <div
        onDrop={onDrop}
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDragEnd={() => setDragging(false)}
        onClick={() => !pending && document.getElementById("ocr-input")?.click()}
        className={[
          "w-full max-w-lg h-60 rounded-2xl border-2 border-dashed",
          "flex flex-col items-center justify-center gap-3 select-none transition-colors",
          pending
            ? "cursor-default opacity-60 border-gray-300 bg-gray-50"
            : dragging
            ? "cursor-copy border-blue-400 bg-blue-50"
            : "cursor-pointer border-gray-300 bg-white hover:border-gray-400 hover:bg-gray-50",
        ].join(" ")}
      >
        <input
          id="ocr-input"
          type="file"
          accept="application/pdf,image/jpeg,image/png"
          className="hidden"
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) handleFile(file);
            e.target.value = "";
          }}
        />

        {pending ? (
          <>
            <div className="w-10 h-10 rounded-full border-4 border-blue-500 border-t-transparent animate-spin" />
            <p className="text-sm text-muted-foreground">Analyse en cours…</p>
          </>
        ) : (
          <>
            <Upload className="w-12 h-12 text-gray-300" />
            <div className="text-center space-y-1">
              <p className="font-medium text-gray-700">Glissez un fichier ici</p>
              <p className="text-sm text-muted-foreground">ou cliquez pour sélectionner</p>
              <p className="text-xs text-muted-foreground">PDF · JPEG · PNG</p>
            </div>
          </>
        )}
      </div>

      {result && (
        <div className="w-full max-w-lg rounded-xl border bg-white shadow-sm">
          <div className="flex items-center justify-between px-5 py-3 border-b">
            <span className="font-semibold text-sm">
              {entries.length > 0
                ? `${entries.length} champ${entries.length > 1 ? "s" : ""} extrait${entries.length > 1 ? "s" : ""}`
                : "Aucune donnée extraite"}
            </span>
            <button
              onClick={() => setResult(null)}
              className="text-muted-foreground hover:text-foreground"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
          {entries.length > 0 ? (
            <ul className="divide-y">
              {entries.map(([key, value]) => (
                <li key={key} className="flex justify-between items-center px-5 py-2.5 text-sm">
                  <span className="text-muted-foreground">
                    {FIELD_LABELS[key] ?? key.replace(/_/g, " ")}
                  </span>
                  <span className="font-medium text-right max-w-[55%] truncate">
                    {String(value)}
                  </span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="px-5 py-4 text-sm text-muted-foreground text-center">
              Le document n'a pas pu être analysé.
            </p>
          )}
        </div>
      )}
    </div>
  );
}
