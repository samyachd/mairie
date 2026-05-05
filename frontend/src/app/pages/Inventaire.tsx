import { useInventaire } from "@/app/hooks/useInventaire";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/app/components/ui/tabs";
import { OrdinateurTable } from "@/app/components/ordinateur/OrdinateurTable";
import { OfficeLicenceTable } from "@/app/components/officelicence/OfficeLicenceTable";
import { EcranTable } from "../components/ecran/EcranTable";
import { AgentTable } from "../components/agent/AgentTable";
import { DocumentTable } from "../components/document/DocumentTable";

export function Inventaire() {
  const { data, isLoading, isError, error } = useInventaire();

  if (isLoading) return <div className="p-6">Chargement...</div>;
  if (isError) {
    return (
      <div className="p-6 text-red-600">
        Erreur : {error instanceof Error ? error.message : "inconnue"}
      </div>
    );
  }
  if (!data) return null;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-6">Inventaire</h1>

      <Tabs defaultValue="ordinateurs">
        <TabsList>
          <TabsTrigger value="ordinateurs">
            Ordinateurs ({data.ordinateurs.length})
          </TabsTrigger>
          <TabsTrigger value="ecrans">
            Écrans ({data.ecrans.length})
          </TabsTrigger>
          <TabsTrigger value="licences">
            Licences ({data.licences.length})
          </TabsTrigger>
          <TabsTrigger value="documents">
            Documents ({data.documents.length})
          </TabsTrigger>
          <TabsTrigger value="agents">
            Agents ({data.agents.length})
          </TabsTrigger>
        </TabsList>

        <TabsContent value="ordinateurs" className="mt-6">
          <OrdinateurTable
            data={data.ordinateurs}
            agents={data.agents}
            documents={data.documents}
          />
        </TabsContent>
        <TabsContent value="ecrans" className="mt-6">
          <EcranTable
            data={data.ecrans}
            agents={data.agents}
            documents={data.documents}
          />
        </TabsContent>
        <TabsContent value="licences" className="mt-6">
          <OfficeLicenceTable
            data={data.licences}
            documents={data.documents}
          />
        </TabsContent>
        <TabsContent value="documents" className="mt-6">
          <DocumentTable
            data={data.documents}
            ordinateurs={data.ordinateurs}
            ecrans={data.ecrans}
            licences={data.licences}
          />
        </TabsContent>
        <TabsContent value="agents" className="mt-6">
          <AgentTable data={data.agents} />
        </TabsContent>
      </Tabs>
    </div>
  );
}
