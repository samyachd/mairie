import { useMemo } from "react";
import { ColumnDef } from "@tanstack/react-table";
import { Trash2, Pencil } from "lucide-react";
import { Button } from "@/app/components/ui/button";
import { useDeleteEcran } from "./useEcran";
import type { Document, DocumentType, Ecran } from "@/app/types";
import { SortableHeader } from "../components/DataTable/SortableHeader";
import { DocumentLink } from "../components/DocumentLink";
import { indexDocsByOwner } from "./useOrdinateurColumns";

interface Options {
  onEdit: (ecran: Ecran) => void;
  documents: Document[];
}

export function useEcranColumns({
  onEdit,
  documents,
}: Options): ColumnDef<Ecran>[] {
  const deleteEcran = useDeleteEcran();
  const docsByEcran = useMemo(
    () => indexDocsByOwner(documents, "ecran_id"),
    [documents]
  );

  const docFor = (id: number, type: DocumentType) =>
    docsByEcran.get(id)?.get(type) ?? null;

  return [
    {
      accessorKey: "taille",
      header: ({ column }) => <SortableHeader column={column} label="Taille" />,
    },
    {
      accessorKey: "marque",
      header: ({ column }) => <SortableHeader column={column} label="Marque" />,
    },
    {
      accessorKey: "slot",
      header: ({ column }) => <SortableHeader column={column} label="Slot" />,
      cell: ({ row }) => row.original.slot ?? "—",
    },
    {
      accessorKey: "proprietaire",
      header: ({ column }) => (
        <SortableHeader column={column} label="Propriétaire" />
      ),
      cell: ({ row }) => row.original.proprietaire ?? "—",
    },
    {
      id: "devis",
      header: "Devis",
      cell: ({ row }) => <DocumentLink doc={docFor(row.original.id, "devis")} />,
    },
    {
      id: "bon_de_commande",
      header: "BC",
      cell: ({ row }) => (
        <DocumentLink doc={docFor(row.original.id, "bon_de_commande")} />
      ),
    },
    {
      id: "facture",
      header: "Facture",
      cell: ({ row }) => <DocumentLink doc={docFor(row.original.id, "facture")} />,
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
              if (confirm(`Supprimer l'écran ${row.original.tag ?? row.original.id} ?`)) {
                deleteEcran.mutate(row.original.id);
              }
            }}
            disabled={deleteEcran.isPending}
          >
            <Trash2 className="h-4 w-4 text-red-600" />
          </Button>
        </div>
      ),
    },
  ];
}
