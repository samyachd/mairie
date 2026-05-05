import { useState } from "react";
import { Plus } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/app/components/ui/dialog";
import { Button } from "@/app/components/ui/button";
import { OrdinateurForm } from "./OrdinateurForm";
import { DocumentForm } from "../document/DocumentForm";
import { useCreateOrdinateur } from "@/app/hooks/useOrdinateur";
import { useCreateDocument } from "@/app/hooks/useDocument";
import type { Agent, Document as DocumentT } from "@/app/types";
import type { OcrExtractedData } from "@/app/services/document";
import {
  isDocumentAlreadyRegistered,
  ocrToDocumentDefaults,
} from "@/app/lib/ocrToDocument";

interface Props {
  agents: Agent[];
  documents: DocumentT[];
}

export function OrdinateurCreateDialog({ agents, documents }: Props) {
  const [open, setOpen] = useState(false);
  const [pendingOcr, setPendingOcr] = useState<OcrExtractedData | null>(null);
  const [createdOrdiId, setCreatedOrdiId] = useState<number | null>(null);

  const createOrdi = useCreateOrdinateur();
  const createDoc = useCreateDocument();

  const reset = () => {
    setPendingOcr(null);
    setCreatedOrdiId(null);
    setOpen(false);
  };

  const handleEquipmentSubmit = (data: Parameters<typeof createOrdi.mutate>[0]) => {
    createOrdi.mutate(data, {
      onSuccess: (ordi) => {
        const docDefaults =
          pendingOcr && !isDocumentAlreadyRegistered(pendingOcr, documents)
            ? ocrToDocumentDefaults(pendingOcr)
            : null;
        if (docDefaults) {
          setCreatedOrdiId(ordi.id);
        } else {
          reset();
        }
      },
    });
  };

  const docDefaults = pendingOcr ? ocrToDocumentDefaults(pendingOcr) : null;
  const showDocStep = createdOrdiId != null && docDefaults != null;

  return (
    <Dialog
      open={open}
      onOpenChange={(o) => {
        if (!o) reset();
        else setOpen(true);
      }}
    >
      <DialogTrigger asChild>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Nouveau
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>
            {showDocStep ? "Document détecté" : "Nouvel ordinateur"}
          </DialogTitle>
          <DialogDescription>
            {showDocStep
              ? "L'OCR a identifié un document non enregistré. Vérifiez et enregistrez-le."
              : "Saisissez les informations de base. Vous pourrez compléter les détails techniques (RAM, OS, IP...) après création."}
          </DialogDescription>
        </DialogHeader>

        {showDocStep ? (
          <DocumentForm
            fixedOwner={{ ordinateur_id: createdOrdiId }}
            defaultValues={docDefaults}
            isPending={createDoc.isPending}
            onSubmit={(data) => {
              createDoc.mutate(data, { onSuccess: reset });
            }}
          />
        ) : (
          <OrdinateurForm
            agents={agents}
            isPending={createOrdi.isPending}
            onOcrExtracted={setPendingOcr}
            onSubmit={handleEquipmentSubmit}
          />
        )}
      </DialogContent>
    </Dialog>
  );
}
