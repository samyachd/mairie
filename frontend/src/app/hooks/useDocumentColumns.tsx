import { useMemo } from "react";
import { ColumnDef } from "@tanstack/react-table";
import type {
  Document,
  DocumentType,
  Ecran,
  OfficeLicence,
  Ordinateur,
} from "@/app/types";
import { SortableHeader } from "../components/DataTable/SortableHeader";
import { DocumentLink } from "../components/DocumentLink";

interface Options {
  ordinateurs: Ordinateur[];
  ecrans: Ecran[];
  licences: OfficeLicence[];
}

const TYPE_LABEL: Record<DocumentType, string> = {
  devis: "Devis",
  bon_de_commande: "Bon de cmd",
  facture: "Facture",
};

function byId<T extends { id: number }>(items: T[]): Map<number, T> {
  return new Map(items.map((item) => [item.id, item]));
}

const fmt = {
  date: (v: string | null | undefined) =>
    v ? new Date(v).toLocaleDateString("fr-FR") : "—",
};

export function useDocumentColumns({
  ordinateurs,
  ecrans,
  licences,
}: Options): ColumnDef<Document>[] {
  const ordiById = useMemo(() => byId(ordinateurs), [ordinateurs]);
  const ecranById = useMemo(() => byId(ecrans), [ecrans]);
  const licenceById = useMemo(() => byId(licences), [licences]);

  const ownerLabel = (doc: Document): string => {
    if (doc.ordinateur_id) {
      const o = ordiById.get(doc.ordinateur_id);
      return `Ordi ${o?.nom_reseau ?? o?.tag ?? `#${doc.ordinateur_id}`}`;
    }
    if (doc.ecran_id) {
      const e = ecranById.get(doc.ecran_id);
      return `Écran ${e?.tag ?? `#${doc.ecran_id}`}`;
    }
    if (doc.office_licence_id) {
      const l = licenceById.get(doc.office_licence_id);
      return `Licence ${l?.version ?? `#${doc.office_licence_id}`}`;
    }
    return "—";
  };

  return [
    {
      accessorKey: "type",
      header: ({ column }) => <SortableHeader column={column} label="Type" />,
      cell: ({ row }) => TYPE_LABEL[row.original.type],
    },
    {
      accessorKey: "numero",
      header: ({ column }) => (
        <SortableHeader column={column} label="Numéro" />
      ),
      cell: ({ row }) => <DocumentLink doc={row.original} />,
    },
    {
      accessorKey: "nom",
      header: ({ column }) => <SortableHeader column={column} label="Nom" />,
    },
    {
      accessorKey: "date_document",
      header: ({ column }) => <SortableHeader column={column} label="Date" />,
      cell: ({ row }) => fmt.date(row.original.date_document),
    },
    {
      id: "owner",
      header: "Lié à",
      cell: ({ row }) => ownerLabel(row.original),
    },
    {
      accessorKey: "montant_ht",
      header: ({ column }) => (
        <SortableHeader column={column} label="Montant HT" />
      ),
      cell: ({ row }) =>
        row.original.montant_ht != null
          ? `${row.original.montant_ht.toFixed(2)} €`
          : "—",
    },
    {
      accessorKey: "montant_ttc",
      header: ({ column }) => (
        <SortableHeader column={column} label="Montant TTC" />
      ),
      cell: ({ row }) =>
        row.original.montant_ttc != null
          ? `${row.original.montant_ttc.toFixed(2)} €`
          : "—",
    },
  ];
}
