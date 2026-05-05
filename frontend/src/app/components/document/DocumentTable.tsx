import { useState, useMemo } from "react";
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
  Document as DocumentT,
  DocumentType,
  Ecran,
  OfficeLicence,
  Ordinateur,
} from "@/app/types";
import { useDocumentColumns } from "@/app/hooks/useDocumentColumns";
import { DocumentCreateDialog } from "./DocumentCreateDialog";
import { DocumentEditDialog } from "./DocumentEditDialog";

interface Props {
  data: DocumentT[];
  ordinateurs: Ordinateur[];
  ecrans: Ecran[];
  licences: OfficeLicence[];
}

type Filter = "all" | DocumentType;

export function DocumentTable({ data, ordinateurs, ecrans, licences }: Props) {
  const [sorting, setSorting] = useState<SortingState>([]);
  const [globalFilter, setGlobalFilter] = useState("");
  const [typeFilter, setTypeFilter] = useState<Filter>("all");
  const [editing, setEditing] = useState<DocumentT | null>(null);

  const filteredData = useMemo(
    () =>
      typeFilter === "all"
        ? data
        : data.filter((d) => d.type === typeFilter),
    [data, typeFilter]
  );

  const columns = useDocumentColumns({
    onEdit: setEditing,
    ordinateurs,
    ecrans,
    licences,
  });

  const table = useReactTable({
    data: filteredData,
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
        <select
          className="border rounded-md px-3 py-2 text-sm"
          value={typeFilter}
          onChange={(e) => setTypeFilter(e.target.value as Filter)}
        >
          <option value="all">Tous les types</option>
          <option value="devis">Devis</option>
          <option value="bon_de_commande">Bons de commande</option>
          <option value="facture">Factures</option>
        </select>
        <div className="text-sm text-gray-500">
          {table.getFilteredRowModel().rows.length} sur {filteredData.length}{" "}
          documents
        </div>
        <div className="ml-auto">
          <DocumentCreateDialog
            ordinateurs={ordinateurs}
            ecrans={ecrans}
            licences={licences}
          />
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

      {editing && (
        <DocumentEditDialog
          document={editing}
          ordinateurs={ordinateurs}
          ecrans={ecrans}
          licences={licences}
          open={true}
          onOpenChange={(open) => {
            if (!open) setEditing(null);
          }}
        />
      )}
    </div>
  );
}
