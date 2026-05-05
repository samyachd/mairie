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
import { DocumentForm } from "./DocumentForm";
import { useCreateDocument } from "@/app/hooks/useDocument";
import type { Ecran, OfficeLicence, Ordinateur } from "@/app/types";

interface Props {
  ordinateurs: Ordinateur[];
  ecrans: Ecran[];
  licences: OfficeLicence[];
}

export function DocumentCreateDialog({ ordinateurs, ecrans, licences }: Props) {
  const [open, setOpen] = useState(false);
  const createMutation = useCreateDocument();

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Nouveau document
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Nouveau document</DialogTitle>
          <DialogDescription>
            Renseignez les informations du document. Vous pouvez le lier à un
            ordinateur, un écran ou une licence (au plus un).
          </DialogDescription>
        </DialogHeader>
        <DocumentForm
          ordinateurs={ordinateurs}
          ecrans={ecrans}
          licences={licences}
          isPending={createMutation.isPending}
          onSubmit={(data) => {
            createMutation.mutate(data, {
              onSuccess: () => setOpen(false),
            });
          }}
        />
      </DialogContent>
    </Dialog>
  );
}
