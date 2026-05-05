import { useMemo } from "react";
import { ColumnDef } from "@tanstack/react-table";
import { Trash2, Pencil } from "lucide-react";
import { Button } from "@/app/components/ui/button";
import { useDeleteOrdinateur } from "./useOrdinateur";
import type { Document, DocumentType, Ordinateur } from "@/app/types";
import { SortableHeader } from "../components/DataTable/SortableHeader";
import { DocumentLink } from "../components/DocumentLink";

interface Options {
  onEdit: (ordinateur: Ordinateur) => void;
  documents: Document[];
}

type DocsByOwner = Map<number, Map<DocumentType, Document>>;

function indexDocsByOwner(
  documents: Document[],
  ownerKey: "ordinateur_id" | "ecran_id" | "office_licence_id"
): DocsByOwner {
  const map: DocsByOwner = new Map();
  for (const doc of documents) {
    const ownerId = doc[ownerKey];
    if (ownerId == null) continue;
    let inner = map.get(ownerId);
    if (!inner) {
      inner = new Map();
      map.set(ownerId, inner);
    }
    const existing = inner.get(doc.type);
    if (!existing || doc.date_document > existing.date_document) {
      inner.set(doc.type, doc);
    }
  }
  return map;
}

export { indexDocsByOwner };

export function useOrdinateurColumns({
  onEdit,
  documents,
}: Options): ColumnDef<Ordinateur>[] {
  const deleteOrdinateur = useDeleteOrdinateur();
  const docsByOrdinateur = useMemo(
    () => indexDocsByOwner(documents, "ordinateur_id"),
    [documents]
  );

  const docFor = (id: number, type: DocumentType) =>
    docsByOrdinateur.get(id)?.get(type) ?? null;

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
