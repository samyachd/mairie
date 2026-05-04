import { useMemo } from "react";
import { ColumnDef } from "@tanstack/react-table";
import { Trash2, Pencil } from "lucide-react";
import { Button } from "@/app/components/ui/button";
import { useDeleteEcran } from "./useEcran";
import type { BonDeCommande, Devis, Ecran, Facture } from "@/app/types";
import { SortableHeader } from "../components/DataTable/SortableHeader";
import { DocumentLink } from "../components/DocumentLink";

interface Options {
  onEdit: (ecran: Ecran) => void;
  devis: Devis[];
  bonsDeCommande: BonDeCommande[];
  factures: Facture[];
}

function byId<T extends { id: number }>(items: T[]): Map<number, T> {
  return new Map(items.map((item) => [item.id, item]));
}

export function useEcranColumns({
  onEdit,
  devis,
  bonsDeCommande,
  factures,
}: Options): ColumnDef<Ecran>[] {
  const deleteEcran = useDeleteEcran();

  const devisById = useMemo(() => byId(devis), [devis]);
  const bcById = useMemo(() => byId(bonsDeCommande), [bonsDeCommande]);
  const factureById = useMemo(() => byId(factures), [factures]);

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
      cell: ({ row }) => (
        <DocumentLink
          doc={row.original.devis_id ? devisById.get(row.original.devis_id) : null}
        />
      ),
    },
    {
      id: "bon_de_commande",
      header: "BC",
      cell: ({ row }) => (
        <DocumentLink
          doc={
            row.original.bon_de_commande_id
              ? bcById.get(row.original.bon_de_commande_id)
              : null
          }
        />
      ),
    },
    {
      id: "facture",
      header: "Facture",
      cell: ({ row }) => (
        <DocumentLink
          doc={
            row.original.facture_id ? factureById.get(row.original.facture_id) : null
          }
        />
      ),
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
