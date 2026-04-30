// hooks/useOrdinateurColumns.tsx
import { ColumnDef } from "@tanstack/react-table";
import { Trash2, Pencil, ArrowUpDown, ArrowUp, ArrowDown } from "lucide-react";
import { Button } from "@/app/components/ui/button";
import { useDeleteOrdinateur } from "./useOrdinateur";
import type { Ordinateur } from "@/app/types";
import { SortableHeader } from "../components/DataTable/SortableHeader";

interface Options {
  onEdit: (ordinateur: Ordinateur) => void;
}

export function useOrdinateurColumns({
  onEdit,
}: Options): ColumnDef<Ordinateur>[] {
  const deleteOrdinateur = useDeleteOrdinateur();

  return [
    {
      accessorKey: "nom_reseau",
      header: ({ column }) => <SortableHeader column={column} label="Nom réseau" />,
    },
    {
      accessorKey: "marque",
      header: ({ column }) => <SortableHeader column={column} label="Marque" />,
    },
    {
      accessorKey: "proprietaire",
      header: ({ column }) => <SortableHeader column={column} label="Propriétaire" />,
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
              if (confirm(`Supprimer l'ordinateur ${row.original.tag} ?`)) {
                deleteOrdinateur.mutate(row.original.id);
              }
            }}
            disabled={deleteOrdinateur.isPending}
          >
            <Trash2 className="h-4 w-4 text-red-600" />
          </Button>
        </div>
      ),
    },
  ];
}