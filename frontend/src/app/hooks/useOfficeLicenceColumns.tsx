import { useMemo } from "react";
import { ColumnDef } from "@tanstack/react-table";
import { Trash2, Pencil } from "lucide-react";
import { Button } from "@/app/components/ui/button";
import { useDeleteOfficeLicence } from "./useOfficeLicence";
import type {
  BonDeCommande,
  Devis,
  Facture,
  OfficeLicence,
} from "@/app/types";
import { SortableHeader } from "../components/DataTable/SortableHeader";
import { DocumentLink } from "../components/DocumentLink";

interface Options {
  onEdit: (licence: OfficeLicence) => void;
  devis: Devis[];
  bonsDeCommande: BonDeCommande[];
  factures: Facture[];
}

function byId<T extends { id: number }>(items: T[]): Map<number, T> {
  return new Map(items.map((item) => [item.id, item]));
}

export function useOfficeLicenceColumns({
  onEdit,
  devis,
  bonsDeCommande,
  factures,
}: Options): ColumnDef<OfficeLicence>[] {
  const deleteLicence = useDeleteOfficeLicence();

  const devisById = useMemo(() => byId(devis), [devis]);
  const bcById = useMemo(() => byId(bonsDeCommande), [bonsDeCommande]);
  const factureById = useMemo(() => byId(factures), [factures]);

  return [
    {
      accessorKey: "version",
      header: ({ column }) => <SortableHeader column={column} label="Version" />,
    },
    {
      accessorKey: "type_licence",
      header: ({ column }) => (
        <SortableHeader column={column} label="Type de licence" />
      ),
      cell: ({ row }) => row.original.type_licence ?? "—",
    },
    {
      accessorKey: "fournisseur",
      header: ({ column }) => (
        <SortableHeader column={column} label="Fournisseur" />
      ),
      cell: ({ row }) => row.original.fournisseur ?? "—",
    },
    {
      accessorKey: "date_achat",
      header: ({ column }) => (
        <SortableHeader column={column} label="Date d'achat" />
      ),
      cell: ({ row }) =>
        row.original.date_achat
          ? new Date(row.original.date_achat).toLocaleDateString("fr-FR")
          : "—",
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
              if (confirm(`Supprimer la licence ${row.original.version} ?`)) {
                deleteLicence.mutate(row.original.id);
              }
            }}
            disabled={deleteLicence.isPending}
          >
            <Trash2 className="h-4 w-4 text-red-600" />
          </Button>
        </div>
      ),
    },
  ];
}
