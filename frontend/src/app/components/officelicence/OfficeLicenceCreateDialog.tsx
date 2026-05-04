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
import { OfficeLicenceForm } from "./OfficeLicenceForm";
import { useCreateOfficeLicence } from "@/app/hooks/useOfficeLicence";

export function OfficeLicenceCreateDialog() {
  const [open, setOpen] = useState(false);
  const createMutation = useCreateOfficeLicence();

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Nouvelle
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Nouvelle licence Office</DialogTitle>
          <DialogDescription>
            Saisissez les informations de la licence. La version est
            obligatoire.
          </DialogDescription>
        </DialogHeader>
        <OfficeLicenceForm
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
