import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/app/components/ui/dialog";
import { OfficeLicenceForm } from "./OfficeLicenceForm";
import { useUpdateOfficeLicence } from "@/app/hooks/useOfficeLicence";
import type { OfficeLicence } from "@/app/types";

interface Props {
  licence: OfficeLicence;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function OfficeLicenceEditDialog({
  licence,
  open,
  onOpenChange,
}: Props) {
  const updateMutation = useUpdateOfficeLicence();

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Modifier {licence.version}</DialogTitle>
          <DialogDescription>
            Modifiez les informations de la licence Office.
          </DialogDescription>
        </DialogHeader>
        <OfficeLicenceForm
          isPending={updateMutation.isPending}
          submitLabel="Enregistrer les modifications"
          defaultValues={{
            version: licence.version,
            type_licence: licence.type_licence,
            date_achat: licence.date_achat,
            fournisseur: licence.fournisseur,
          }}
          onSubmit={(data) => {
            updateMutation.mutate(
              { id: licence.id, data },
              {
                onSuccess: () => onOpenChange(false),
              }
            );
          }}
        />
      </DialogContent>
    </Dialog>
  );
}
