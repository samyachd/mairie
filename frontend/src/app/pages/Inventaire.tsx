// src/app/pages/Inventaire.tsx
import { useInventaire } from "@/app/hooks/useInventaire";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/app/components/ui/tabs";
import { OrdinateursTable } from "@/app/components/OrdinateurTable";
import { OfficeLicencesTable } from "@/app/components/officelicence/OfficeLicenceTable";
import { EcransTable } from "../components/ecran/EcranTable";
import { AgentsTable } from "../components/AgentTable";
import { DevisTable } from "../components/devis/DevisTable";
import { FacturesTable } from "../components/facture/FactureTable";
import { BonsDeCommandeTable } from "../components/bondecommande/BonDeCommandeTable";

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
          <TabsTrigger value="devis">
            Devis ({data.devis.length})
          </TabsTrigger>
          <TabsTrigger value="bons_de_commande">
            Bons de commande ({data.bons_de_commande.length})
          </TabsTrigger>
          <TabsTrigger value="factures">
            Factures ({data.factures.length})
          </TabsTrigger>
          <TabsTrigger value = "agents">
            Agents ({data.agents.length})
          </TabsTrigger>
        </TabsList>

        <TabsContent value="ordinateurs" className="mt-6">
          <OrdinateursTable data={data.ordinateurs} agents={data.agents} />
        </TabsContent>
        <TabsContent value="ecrans" className="mt-6">
          <EcransTable data={data.ecrans} />
        </TabsContent>
        <TabsContent value="licences" className="mt-6">
          <OfficeLicencesTable data={data.licences} />
        </TabsContent>
        <TabsContent value="devis" className="mt-6">
          <DevisTable data={data.devis} />
        </TabsContent>
        <TabsContent value="bons_de_commande" className="mt-6">
          <BonsDeCommandeTable data={data.bons_de_commande} />
        </TabsContent>
        <TabsContent value="factures" className="mt-6">
          <FacturesTable data={data.factures} />
        </TabsContent>
        <TabsContent value="agents" className="mt-6">
          <AgentsTable data={data.agents} />
        </TabsContent>
      </Tabs>
    </div>
  );
}