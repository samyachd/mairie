import { ColumnDef } from "@tanstack/react-table";
import { Button } from "@/app/components/ui/button";
import { useDeleteAgent } from "./useAgent";
import type { Agent } from "@/app/types";
import { Trash2, Pencil } from "lucide-react";
import { SortableHeader } from "../components/DataTable/SortableHeader";

interface Options {
  onEdit: (agent: Agent) => void;
}

export function useAgentColumns({ onEdit }: Options): ColumnDef<Agent>[] {
  const deleteAgent = useDeleteAgent();

  return [
    {
      accessorKey: "nom",
      header: ({ column }) => <SortableHeader column={column} label="Nom" />,
    },
    {
      accessorKey: "prenom",
      header: ({ column }) => <SortableHeader column={column} label="Prénom" />,
    },
    {
      accessorKey: "service",
      header: ({ column }) => <SortableHeader column={column} label="Service" />,
    },
    {
      accessorKey: "email",
      header: "Email",
      cell: ({ row }) => row.original.email ?? "—",
    },
    {
      accessorKey: "telephone",
      header: "Téléphone",
      cell: ({ row }) => row.original.telephone ?? "—",
    },
    {
      id: "actions",
      header: "",
      cell: ({ row }) => (
        <div className="flex items-center gap-1">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => onEdit(row.original)}
          >
            <Pencil className="h-4 w-4" />
          </Button>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => {
              const fullName = `${row.original.prenom} ${row.original.nom}`;
              if (confirm(`Supprimer l'agent ${fullName} ?`)) {
                deleteAgent.mutate(row.original.id);
              }
            }}
            disabled={deleteAgent.isPending}
          >
            <Trash2 className="h-4 w-4 text-red-600" />
          </Button>
        </div>
      ),
    },
  ];
}