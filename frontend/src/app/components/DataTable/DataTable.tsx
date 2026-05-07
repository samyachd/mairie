import { useState, ReactNode } from "react";
import {
  ColumnDef,
  Row,
  RowSelectionState,
  SortingState,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
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
import { Input } from "@/app/components/ui/input";
import { Button } from "@/app/components/ui/button";
import { Checkbox } from "@/app/components/ui/checkbox";
import { Pencil, Trash2 } from "lucide-react";

interface Props<T> {
  data: T[];
  columns: ColumnDef<T>[];
  searchPlaceholder?: string;
  itemLabel?: string;
  toolbarLeft?: ReactNode;
  toolbarRight?: ReactNode;
  onEdit?: (row: T) => void;
  onDelete?: (rows: T[]) => void;
}

export function DataTable<T>({
  data,
  columns,
  searchPlaceholder = "Rechercher...",
  itemLabel = "éléments",
  toolbarLeft,
  toolbarRight,
  onEdit,
  onDelete,
}: Props<T>) {
  const [sorting, setSorting] = useState<SortingState>([]);
  const [globalFilter, setGlobalFilter] = useState("");
  const [rowSelection, setRowSelection] = useState<RowSelectionState>({});
  const [lastSelectedIndex, setLastSelectedIndex] = useState<number | null>(null);

  const handleSelect = (
    e: React.MouseEvent,
    row: Row<T>,
    rowIndex: number
  ) => {
    if (e.shiftKey && lastSelectedIndex !== null) {
      e.preventDefault();
      const rows = table.getRowModel().rows;
      const start = Math.min(lastSelectedIndex, rowIndex);
      const end = Math.max(lastSelectedIndex, rowIndex);
      const next: RowSelectionState = {};
      for (let i = start; i <= end; i++) {
        next[rows[i].id] = true;
      }
      setRowSelection(next);
    } else {
      row.toggleSelected();
    }
    setLastSelectedIndex(rowIndex);
  };

  const selectColumn: ColumnDef<T> = {
    id: "select",
    header: ({ table }) => (
      <Checkbox
        checked={
          table.getIsAllPageRowsSelected() ||
          (table.getIsSomePageRowsSelected() ? "indeterminate" : false)
        }
        onCheckedChange={(v) => table.toggleAllRowsSelected(!!v)}
        aria-label="Tout sélectionner"
      />
    ),
    cell: ({ row }) => {
      const rows = table.getRowModel().rows;
      const rowIndex = rows.findIndex((r) => r.id === row.id);
      return (
        <div
          onClick={(e) => {
            e.stopPropagation();
            handleSelect(e, row, rowIndex);
          }}
        >
          <Checkbox
            checked={row.getIsSelected()}
            aria-label="Sélectionner"
          />
        </div>
      );
    },
    enableSorting: false,
    enableGlobalFilter: false,
  };

  const allColumns: ColumnDef<T>[] = [selectColumn, ...columns];

  const table = useReactTable({
    data,
    columns: allColumns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onSortingChange: setSorting,
    onGlobalFilterChange: setGlobalFilter,
    onRowSelectionChange: setRowSelection,
    state: { sorting, globalFilter, rowSelection },
    enableRowSelection: true,
  });

  const selectedRows = table.getSelectedRowModel().rows;
  const selectedCount = selectedRows.length;

  const handleEdit = () => {
    if (selectedCount === 1 && onEdit) {
      onEdit(selectedRows[0].original);
      setRowSelection({});
    }
  };

  const handleDelete = () => {
    if (selectedCount > 0 && onDelete) {
      onDelete(selectedRows.map((r) => r.original));
      setRowSelection({});
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-4">
        <Input
          placeholder={searchPlaceholder}
          value={globalFilter}
          onChange={(e) => setGlobalFilter(e.target.value)}
          className="max-w-sm"
        />
        {toolbarLeft}
        <div className="text-sm text-muted-foreground">
          {selectedCount > 0 && (
            <span className="font-medium">
              {selectedCount} sélectionné{selectedCount > 1 ? "s" : ""} /{" "}
            </span>
          )}
          {table.getFilteredRowModel().rows.length} / {data.length} {itemLabel}
        </div>
        <div className="ml-auto flex items-center gap-2">
          {onEdit && (
            <Button
              variant="outline"
              size="sm"
              onClick={handleEdit}
              disabled={selectedCount !== 1}
            >
              <Pencil className="h-4 w-4 mr-1" />
              Modifier
            </Button>
          )}
          {onDelete && (
            <Button
              variant="outline"
              size="sm"
              onClick={handleDelete}
              disabled={selectedCount === 0}
            >
              <Trash2 className="h-4 w-4 mr-1 text-red-500" />
              Supprimer
            </Button>
          )}
          {toolbarRight}
        </div>
      </div>

      <div className="rounded-md border overflow-hidden">
        <div className="overflow-auto max-h-[68vh]">
          <Table className="min-w-max">
            <TableHeader className="sticky top-0 z-10 bg-background shadow-sm">
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
                table.getRowModel().rows.map((row, rowIndex) => (
                  <TableRow
                    key={row.id}
                    data-state={row.getIsSelected() ? "selected" : undefined}
                    className="cursor-pointer"
                    onClick={(e) => handleSelect(e, row, rowIndex)}
                  >
                    {row.getVisibleCells().map((cell) => (
                      <TableCell key={cell.id}>
                        {flexRender(
                          cell.column.columnDef.cell,
                          cell.getContext()
                        )}
                      </TableCell>
                    ))}
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell
                    colSpan={allColumns.length}
                    className="h-24 text-center text-muted-foreground"
                  >
                    Aucun résultat.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>
      </div>
    </div>
  );
}
