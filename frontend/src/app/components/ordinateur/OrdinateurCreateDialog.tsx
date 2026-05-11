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
import { useCreateOrdinateur } from "@/app/hooks/useOrdinateur";
import type { Agent } from "@/app/types";

interface Props {
  agents: Agent[];
  disabled?: boolean;
}

export function OrdinateurCreateDialog({ agents, disabled }: Props) {
  const [open, setOpen] = useState(false);
  const createOrdi = useCreateOrdinateur();

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button disabled={disabled}>
          <Plus className="h-4 w-4 mr-2" />
          Nouveau
        </Button>
      </DialogTrigger>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Nouvel ordinateur</DialogTitle>
          <DialogDescription>
            Saisissez les informations de l'ordinateur.
          </DialogDescription>
        </DialogHeader>
        <OrdinateurForm
          agents={agents}
          isPending={createOrdi.isPending}
          onSubmit={(data) =>
            createOrdi.mutate(data, { onSuccess: () => setOpen(false) })
          }
        />
      </DialogContent>
    </Dialog>
  );
}
