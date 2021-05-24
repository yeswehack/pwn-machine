import gql from "graphql-tag";
import { IMAGE_FRAGMENT } from "./fragments.js";

export const LIST_IMAGES = gql`
  query listImages($onlyFinal: Boolean = true) {
    dockerImages(onlyFinal: $onlyFinal) {
      ...ImageFragment
    }
  }
  ${IMAGE_FRAGMENT}
`;

export const SEARCH_IMAGE = gql`
  query dockerSearchImage($search: String!) {
    dockerSearchImage(search: $search) {
      name
      description
      starCount
      isOfficial
      isAutomated
    }
  }
`;

export const SEARCH_IMAGE_TAG = gql`
  query dockerSearchImageTag($repoName: String!, $imageName: String!) {
    dockerSearchImageTag(repoName: $repoName, imageName: $imageName) {
      name
      size
      lastUpdated
    }
  }
`;
