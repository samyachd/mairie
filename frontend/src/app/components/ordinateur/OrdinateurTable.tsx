import { useState } from "react";
import type { Agent, Document, Ordinateur } from "@/app/types";
import { useOrdinateurColumns } from "@/app/hooks/useOrdinateurColumns";
import { useDeleteOrdinateur } from "@/app/hooks/useOrdinateur";
import { OrdinateurCreateDialog } from "./OrdinateurCreateDialog";
import { OrdinateurOcrDialog } from "./OrdinateurOcrDialog";
import { OrdinateurEditDialog } from "./OrdinateurEditDialog";
import { DataTable } from "../DataTable/DataTable";

interface Props {
  data: Ordinateur[];
  agents: Agent[];
  documents: Document[];
}

export function OrdinateurTable({ data, agents, documents }: Props) {
  const [editingOrdinateur, setEditingOrdinateur] = useState<Ordinateur | null>(null);
  const deleteOrdinateur = useDeleteOrdinateur();

  const columns = useOrdinateurColumns({ agents, documents });

  return (
    <>
      <DataTable
        data={data}
        columns={columns}
        searchPlaceholder="Rechercher un ordinateur..."
        itemLabel="ordinateurs"
        onEdit={setEditingOrdinateur}
        onDelete={(rows) => {
          const msg =
            rows.length === 1
              ? `Supprimer l'ordinateur ${rows[0].tag ?? rows[0].id} ?`
              : `Supprimer ${rows.length} ordinateurs ?`;
          if (confirm(msg)) rows.forEach((r) => deleteOrdinateur.mutate(r.id));
        }}
        toolbarRight={
          <div className="flex gap-2">
            <OrdinateurOcrDialog agents={agents} documents={documents} />
            <OrdinateurCreateDialog agents={agents} />
          </div>
        }
      />
      {editingOrdinateur && (
        <OrdinateurEditDialog
          ordinateur={editingOrdinateur}
          agents={agents}
          documents={documents}
          open={true}
          onOpenChange={(open) => {
            if (!open) setEditingOrdinateur(null);
          }}
        />
      )}
    </>
  );
}
