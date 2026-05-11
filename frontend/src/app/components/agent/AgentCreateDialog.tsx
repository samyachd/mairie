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
import { AgentForm } from "./AgentForm";
import { useCreateAgent } from "@/app/hooks/useAgent";

export function AgentCreateDialog({ disabled }: { disabled?: boolean }) {
  const [open, setOpen] = useState(false);
  const createMutation = useCreateAgent();

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button disabled={disabled}>
          <Plus className="h-4 w-4 mr-2" />
          Nouveau
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Nouvel agent</DialogTitle>
          <DialogDescription>
            Saisissez les informations de l'agent. Le nom et le prénom sont
            obligatoires.
          </DialogDescription>
        </DialogHeader>
        <AgentForm
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