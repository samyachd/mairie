import { ColumnDef } from "@tanstack/react-table";
import type { Agent } from "@/app/types";
import { SortableHeader } from "../components/DataTable/SortableHeader";

export function useAgentColumns(): ColumnDef<Agent>[] {
  return [
    {
      accessorKey: "nom",
      header: ({ column }) => <SortableHeader column={column} label="Nom" />,
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
  ];
}
