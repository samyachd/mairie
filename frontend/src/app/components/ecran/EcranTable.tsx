import { useState } from "react";
import type { Agent, Document, Ecran, Ordinateur } from "@/app/types";
import { useEcranColumns } from "@/app/hooks/useEcranColumns";
import { useDeleteEcran } from "@/app/hooks/useEcran";
import { EcranCreateDialog } from "./EcranCreateDialog";
import { EcranOcrDialog } from "./EcranOcrDialog";
import { EcranEditDialog } from "./EcranEditDialog";
import { DataTable } from "../DataTable/DataTable";

interface Props {
  data: Ecran[];
  agents: Agent[];
  ordinateurs: Ordinateur[];
  documents: Document[];
}

export function EcranTable({ data, agents, ordinateurs, documents }: Props) {
  const [editingEcran, setEditingEcran] = useState<Ecran | null>(null);
  const deleteEcran = useDeleteEcran();

  const columns = useEcranColumns({ agents, ordinateurs, documents });

  return (
    <>
      <DataTable
        data={data}
        columns={columns}
        searchPlaceholder="Rechercher un écran..."
        itemLabel="écrans"
        onEdit={setEditingEcran}
        onDelete={(rows) => {
          const msg =
            rows.length === 1
              ? `Supprimer l'écran ${rows[0].tag ?? rows[0].id} ?`
              : `Supprimer ${rows.length} écrans ?`;
          if (confirm(msg)) rows.forEach((r) => deleteEcran.mutate(r.id));
        }}
        toolbarRight={
          <div className="flex gap-2">
            <EcranOcrDialog agents={agents} ordinateurs={ordinateurs} documents={documents} />
            <EcranCreateDialog agents={agents} ordinateurs={ordinateurs} />
          </div>
        }
      />
      {editingEcran && (
        <EcranEditDialog
          ecran={editingEcran}
          agents={agents}
          ordinateurs={ordinateurs}
          documents={documents}
          open={true}
          onOpenChange={(open) => {
            if (!open) setEditingEcran(null);
          }}
        />
      )}
    </>
  );
}
