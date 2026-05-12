import { useState } from "react";
import { type ColumnDef } from "@tanstack/react-table";
import { Badge } from "@/app/components/ui/badge";
import { DataTable } from "@/app/components/DataTable/DataTable";
import { UserCreateDialog } from "./UserCreateDialog";
import { UserEditDialog } from "./UserEditDialog";
import { useDeleteUser } from "@/app/hooks/useUser";
import type { UserRecord } from "@/app/services/user";

const ROLE_STYLE: Record<string, string> = {
  admin: "bg-red-100 text-red-800",
  user:  "bg-blue-100 text-blue-800",
  read:  "bg-gray-100 text-gray-700",
};

const ROLE_LABEL: Record<string, string> = {
  admin: "Administrateur",
  user:  "Utilisateur",
  read:  "Lecture seule",
};

const columns: ColumnDef<UserRecord>[] = [
  { accessorKey: "id", header: "ID", cell: ({ getValue }) => <span className="font-mono text-xs">#{getValue() as number}</span> },
  { accessorKey: "nom", header: "Nom" },
  { accessorKey: "email", header: "Email" },
  {
    accessorKey: "role",
    header: "Rôle",
    cell: ({ getValue }) => {
      const role = getValue() as string;
      return (
        <Badge className={`${ROLE_STYLE[role] ?? ""} hover:opacity-80`}>
          {ROLE_LABEL[role] ?? role}
        </Badge>
      );
    },
  },
];

interface Props {
  data: UserRecord[];
}

export function UserTable({ data }: Props) {
  const [editing, setEditing] = useState<UserRecord | null>(null);
  const deleteUser = useDeleteUser();

  return (
    <>
      <DataTable
        data={data}
        columns={columns}
        searchPlaceholder="Rechercher un utilisateur…"
        itemLabel="utilisateurs"
        onEdit={setEditing}
        onDelete={(rows) => {
          const msg = rows.length === 1
            ? `Supprimer l'utilisateur ${rows[0].nom} ?`
            : `Supprimer ${rows.length} utilisateurs ?`;
          if (confirm(msg)) rows.forEach((r) => deleteUser.mutate(r.id));
        }}
        toolbarRight={<UserCreateDialog />}
      />
      {editing && (
        <UserEditDialog
          user={editing}
          open={true}
          onOpenChange={(open) => { if (!open) setEditing(null); }}
        />
      )}
    </>
  );
}
