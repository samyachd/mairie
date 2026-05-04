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
}

export function OrdinateurCreateDialog({ agents }: Props) {
  const [open, setOpen] = useState(false);
  const createMutation = useCreateOrdinateur();

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button>
          <Plus className="h-4 w-4 mr-2" />
          Nouveau
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Nouvel ordinateur</DialogTitle>
          <DialogDescription>
            Saisissez les informations de base. Vous pourrez compléter les
            détails techniques (RAM, OS, IP...) après création.
          </DialogDescription>
        </DialogHeader>
        <OrdinateurForm
          agents={agents}
          isPending={createMutation.isPending}
          onSubmit={(data) => {
            createMutation.mutate(data, {
              onSuccess: () => {
                setOpen(false);
              },
            });
          }}
        />
      </DialogContent>
    </Dialog>
  );
}