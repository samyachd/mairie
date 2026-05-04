import { useState } from "react";
import {
  SortingState,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from "@tanstack/react-table";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/app/components/ui/table";
import { Button } from "@/app/components/ui/button";
import { Input } from "@/app/components/ui/input";
import type {
  Agent,
  BonDeCommande,
  Devis,
  Facture,
  Ordinateur,
} from "@/app/types";
import { useOrdinateurColumns } from "@/app/hooks/useOrdinateurColumns";
import { OrdinateurCreateDialog } from "./OrdinateurCreateDialog";
import { OrdinateurEditDialog } from "./OrdinateurEditDialog";

interface Props {
  data: Ordinateur[];
  agents: Agent[];
  devis: Devis[];
  bonsDeCommande: BonDeCommande[];
  factures: Facture[];
}

export function OrdinateurTable({
  data,
  agents,
  devis,
  bonsDeCommande,
  factures,
}: Props) {
  const [sorting, setSorting] = useState<SortingState>([]);
  const [globalFilter, setGlobalFilter] = useState("");
  const [editingOrdinateur, setEditingOrdinateur] =
    useState<Ordinateur | null>(null);

  const columns = useOrdinateurColumns({
    onEdit: (ordinateur) => setEditingOrdinateur(ordinateur),
    devis,
    bonsDeCommande,
    factures,
  });

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    onSortingChange: setSorting,
    onGlobalFilterChange: setGlobalFilter,
    state: { sorting, globalFilter },
    initialState: { pagination: { pageSize: 10 } },
  });

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-4">
        <Input
          placeholder="Rechercher..."
          value={globalFilter}
          onChange={(event) => setGlobalFilter(event.target.value)}
          className="max-w-sm"
        />
        <div className="text-sm text-gray-500">
          {table.getFilteredRowModel().rows.length} sur {data.length} ordinateurs
        </div>
        <div className="ml-auto">
          <OrdinateurCreateDialog agents={agents} />
        </div>
      </div>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <TableHead key={header.id}>
                    {flexRender(
                      header.column.columnDef.header,
                      header.getContext()
                    )}
                  </TableHead>
                ))}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows.length > 0 ? (
              table.getRowModel().rows.map((row) => (
                <TableRow key={row.id}>
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center text-gray-500"
                >
                  Aucun résultat.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>

        <div className="flex items-center justify-between py-4">
          <div className="text-sm text-gray-500">
            Page {table.getState().pagination.pageIndex + 1} sur{" "}
            {table.getPageCount()}
          </div>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => table.previousPage()}
              disabled={!table.getCanPreviousPage()}
            >
              Précédent
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => table.nextPage()}
              disabled={!table.getCanNextPage()}
            >
              Suivant
            </Button>
          </div>
        </div>
      </div>

      
      {editingOrdinateur && (
        <OrdinateurEditDialog
          ordinateur={editingOrdinateur}
          agents={agents}
          open={true}
          onOpenChange={(open) => {
            if (!open) setEditingOrdinateur(null);
          }}
        />
      )}
    </div>
  );
}